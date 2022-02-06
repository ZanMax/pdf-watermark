<template>
  <div>
    <b-container>
      <form v-on:submit.prevent="submitForm">
        <b-row>
          <b-col sm="8">
            <img src="../assets/pdf_tools.png" alt="pdf tools">
          </b-col>
        </b-row>
        <b-row>
          <b-col sm="6">
            <div class="form-group type-select">
              <b-form-select v-model="selected" :options="options"></b-form-select>
            </div>
          </b-col>
        </b-row>
        <b-row>
          <b-col sm="9">
            <div class="step1">STEP 1</div>
            <b-row>
              <b-col cols="8" sm="6">
                <div class="form-group">
                  <label for="docxfile">Docx file: </label>
                  <input type="file" id="docxfile" ref="docxfile" v-on:change="docxUpload()" accept=".docx"/>
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col cols="4" sm="6">
                <div class="form-group">
                  <label for="watermarkfile">Watermark: </label>
                  <input type="file" id="watermarkfile" ref="watermarfile" v-on:change="watermarkUpload()"
                         accept=".jpg"/>
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <b-row>
          <b-col sm="9">
            <div class="step2">STEP 2</div>
            <b-row>
              <b-col cols="8" sm="6">
                <div class="form-group">
                  <label for="logofile">Logo file: </label>
                  <input type="file" id="logofile" ref="logofile" v-on:change="logoUpload()" accept=".png,.jpg"/>
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col cols="4" sm="6">
                <div class="form-group">
                  <div class="headerText">
                    <label for="headertext">Header text: </label>
                    <input v-model="headertext" id="headertext" placeholder="Head text" size="30"/>
                  </div>
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <b-row>
          <b-col sm="9">
            <div class="step3">STEP 3</div>
            <b-row>
              <b-col cols="8" sm="6">
                <div class="form-group">
                  <label for="convertimage">Convert: </label>
                  <input type="file" id="convertimage" ref="convertfile" v-on:change="convertUpload()"
                         accept=".png,.jpg"/>
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col cols="4" sm="6">
                <div class="form-group">
                  <div class="convertUrl">
                    <label for="converturl">Convert URL: </label>
                    <input v-model="converturl" id="converturl" placeholder="URL" size="30"/>
                  </div>
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="8">
            <div class="form-group">
              <div class="buttonblock">
                <button id="createPdfButton" v-show="!btnHidden" type="button" class="btn btn-primary"
                        v-on:click="submitForm()">Create
                  PDF
                </button>
                <b-button variant="primary" disabled v-show="btnHidden">
                  <b-spinner small type="grow"></b-spinner>
                  Loading...
                </b-button>
              </div>
            </div>
          </b-col>
        </b-row>
      </form>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  title: 'Watermark PDF Generator',
  name: "PdfCheck",
  data() {
    return {
      converturl: '',
      headertext: '',
      docx: '',
      watermark: '',
      logo: '',
      convert: '',
      btnHidden: false,
      selected: '1',
      options: [
        {value: '1', text: 'Standard'},
        {value: '2', text: 'Center'},
      ]
    }
  },
  methods: {
    submitForm() {
      this.btnHidden = true
      let formData = new FormData();
      formData.append('headertext', this.headertext)
      formData.append('converturl', this.converturl)
      formData.append('docx', this.docx)
      formData.append('watermark', this.watermark)
      formData.append('logo', this.logo)
      formData.append('convert', this.convert)
      formData.append('convert_type', this.selected)

      axios.post('/api/doc/create', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
          .then((res) => {
            this.downloadFile(res, 'final_wtm')
          })
          .catch((error) => {
            console.log(error)
          }).finally(() => {
        this.btnHidden = false
        this.converturl = ''
        this.headertext = ''
        this.$refs.convertfile.value = null
        this.$refs.logofile.value = null
        this.$refs.watermarfile.value = null
        this.$refs.docxfile.value = null
      });

    },
    docxUpload() {
      this.docx = this.$refs.docxfile.files[0]
    },
    watermarkUpload() {
      this.watermark = this.$refs.watermarfile.files[0]
    },
    logoUpload() {
      this.logo = this.$refs.logofile.files[0]
    },
    convertUpload() {
      this.convert = this.$refs.convertfile.files[0]
    },
    downloadFile(response) {
      let link = document.createElement('a');
      link.innerHTML = 'Download PDF file'
      link.download = response.data.filename
      link.href = 'data:application/octet-stream;base64,' + response.data.file_blob
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },

  }
}
</script>

<style scoped>
.buttonblock {
  padding-top: 20px;
}

label {
  padding: 5px;
}

.convertUrl {
  text-align: left;
}

.headerText {
  text-align: left;
}

.step1 {
  color: maroon;
  font-weight: 600;
  padding-top: 20px;
}

.step2 {
  color: maroon;
  font-weight: 600;
  padding-top: 20px;
}

.step3 {
  color: maroon;
  font-weight: 600;

}

.type-select {
  padding-top: 20px;
}
</style>